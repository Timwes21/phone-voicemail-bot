import Fastify from 'fastify';
import WebSocket from 'ws';
import { connect } from '@ngrok/ngrok';
import dotenv from 'dotenv';
import fastifyFormBody from '@fastify/formbody';
import fastifyWs from '@fastify/websocket';
import { getTwimlResponse, sendSessionUpdate } from './helper.js';
try{

    const log = (e) => console.log(e);
    const AgentActionsApi = "http://127.0.0.1:3000";


    dotenv.config();
    const { OPENAI_KEY } = process.env;
    const { NGROK_TOKEN } = process.env
    const PORT = process.env.PORT || 5050; 
    OPENAI_KEY ?? console.error('Missing OpenAI API key. Please set it in the .env file.');
    
    const fastify = Fastify();
    fastify.register(fastifyFormBody);
    fastify.register(fastifyWs);


    
    let callerId = ''
    fastify.all('/incoming-call', async (request, reply) => {
        console.log("here");
        callerId = request.body.Caller;
        try{
            const twimlResponse = getTwimlResponse("You are being transferred to Tim's AI Assistant", request)
            reply.type('text/xml').send(twimlResponse);
        }
        catch(err){
            console.log(err);
        }
    });   
    
    fastify.register(async (fastify) => {
        fastify.get('/media-stream', { websocket: true }, (connection, req) => {
            log('Client connected');
            
            try{
                const convo = []
                let streamSid = null;

                const openAiWs = new WebSocket('wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01', {
                    headers: {
                    Authorization: `Bearer ${OPENAI_KEY}`,
                    "OpenAI-Beta": "realtime=v1"
                    }
                });
                
                openAiWs.on('open', () => {
                    log('Connected to the OpenAI Realtime API');
                    setTimeout(()=>sendSessionUpdate(openAiWs), 250); 
                });

                openAiWs.on('message', (messageFromAI) => {
                    try {
                        const parsesMessageFromAI = JSON.parse(messageFromAI);
                        const { type, delta, transcript } = parsesMessageFromAI
                        if (type === 'response.audio.delta' && delta) {
                            const audioDelta = {
                                event: 'media',
                                streamSid: streamSid,
                                media: { payload: Buffer.from(delta, 'base64').toString('base64') }
                            };
                            connection.send(JSON.stringify(audioDelta));
                        }
                        if (type === 'conversation.item.input_audio_transcription.completed'){
                            log('here');
                            convo.push({"caller": transcript})
                        }
                        if( type === 'response.audio_transcript.done'){
                            log('here');
                            convo.push({"AI": transcript})
                            
                        }

                    } catch (error) {
                        console.error('Error processing OpenAI message:', error);
                    }
                });
    
                connection.on('message', async(messageFromCaller) => {
                    try {
                        const parsedMessageFromCaller = JSON.parse(messageFromCaller);
                        const { event, media, start } = parsedMessageFromCaller
                        switch (parsedMessageFromCaller.event) {
                            case 'media':
                                if (openAiWs.readyState === WebSocket.OPEN) {
                                    const audioAppend = {
                                        type: 'input_audio_buffer.append',
                                        audio: media.payload
                                    };

                                    const audioAppendStringify = JSON.stringify(audioAppend)
                                    openAiWs.send(audioAppendStringify);
                                }
                                break;
                            case 'start':
                                streamSid = start.streamSid;
                                log('Incoming stream has started ' + streamSid);
                                break;
                            case "stop":
                                await fetch(AgentActionsApi, {
                                    method: "POST",
                                    headers: {"Content-Type": "application/json"},
                                    body: JSON.stringify({convo: convo, callerId: callerId})
                                })
                                break;
                            default:
                                log('Received non-media event: ' +  event);
                                break;
                        }
                    } catch (error) {
                        console.error('Error parsing message:', error, 'Message:', messageFromCaller);
                    }
                });
                // Handle connection close
                connection.on('close', () => {
                    if (openAiWs.readyState === WebSocket.OPEN) openAiWs.close();
                    log('Client disconnected.');
                });
                // Handle WebSocket close and errors
                openAiWs.on('close', () => {
                    log('Disconnected from the OpenAI Realtime API');
                });
                openAiWs.on('error', (error) => {
                    console.error('Error in the OpenAI WebSocket:', error);
                });
            }
            catch(err){
                log(err);
                
            }
        });
    });


    fastify.listen({ port: PORT, host: "0.0.0.0" }, (err) => {
        if (err) {
            console.error(err);
            process.exit(1);
        }
        console.log(`Server is listening on port ${PORT}`);
    });
    const url = await connect({ addr: PORT, authtoken: NGROK_TOKEN }); // Automatically creates a tunnel
    console.log(`Fastify listening on localhost:${PORT}`);
    console.log(`Ngrok tunnel available at: ${url.url()}`);
}
catch(err){
    console.log(err);
    
}