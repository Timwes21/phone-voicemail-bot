import Fastify from 'fastify';
import WebSocket from 'ws';
import fs from 'fs';
import dotenv from 'dotenv';
import fastifyFormBody from '@fastify/formbody';
import fastifyWs from '@fastify/websocket';
import { OpenAIWS } from './openai-websockets.js';
try{


    // Load environment variables from .env file
    dotenv.config();
    // Retrieve the OpenAI API key from environment variables. You must have OpenAI Realtime API access.
    const { OPENAI_KEY } = process.env;
    if (!OPENAI_KEY) {
        console.error('Missing OpenAI API key. Please set it in the .env file.');
        process.exit(1);
    }
    // Initialize Fastify
    const fastify = Fastify();
    fastify.register(fastifyFormBody);
    fastify.register(fastifyWs);

    // Constants
    const SYSTEM_MESSAGE = 'You are a helpful and bubbly AI assistant who loves to chat about anything the user is interested about and is prepared to offer them facts. You have a penchant for dad jokes, owl jokes, and rickrolling – subtly. Always stay positive, but work in a joke when appropriate.';
    const VOICE = 'alloy';
    const PORT = process.env.PORT || 5050; // Allow dynamic port assignment
    console.log(PORT);

    // List of Event Types to log to the console. See OpenAI Realtime API Documentation. (session.updated is handled separately.)
    const LOG_EVENT_TYPES = [
        'response.content.done',
        'rate_limits.updated',
        'response.done',
        'input_audio_buffer.committed',
        'input_audio_buffer.speech_stopped',
        'input_audio_buffer.speech_started',
        'session.created'
    ];

    fastify.get('/', async (request, reply) => {
        reply.send({ message: 'Twilio Media Stream Server is running!' });
    });
    try{
        fastify.all('/incoming-call', async (request, reply) => {
            console.log("here");
            const twimlResponse = `<?xml version="1.0" encoding="UTF-8"?>
            <Response>
            <Say>Please wait while we connect your call to the A. I. voice assistant, powered by Twilio and the Open-A.I. Realtime API</Say>
            <Pause length="1"/>
            <Say>O.K. you can start talking!</Say>
            <Connect>
            <Stream url="wss://phone-voicemail-bot-production.up.railway.app/media-stream" />
            </Connect>
            </Response>`;
            reply.type('text/xml').send(twimlResponse);
        });   
    }
    catch(err){
        console.log(err);
        
    }
    // WebSocket route for media-stream
    fastify.register(async (fastify) => {
        fastify.get('/media-stream', { websocket: true }, (connection, req) => {
            console.log('Client connected');
            let streamSid = null;

            const openAiWs = new OpenAIWS(OPENAI_KEY);
            openAiWs.onOpen();
            openAiWs.onMsg(connection);

            // Handle incoming messages from Twilio
            connection.on('message', (message) => {
                try {
                    const data = JSON.parse(message);
                    switch (data.event) {
                        case 'media':
                            if (openAiWs.ws.readyState === WebSocket.OPEN) {
                                const audioAppend = {
                                    type: 'input_audio_buffer.append',
                                    audio: data.media.payload
                                };
                                const reply = JSON.stringify(audioAppend)
                                console.log(reply);
                                openAiWs.send(reply);
                            }
                            break;
                        case 'start':
                            streamSid = data.start.streamSid;
                            console.log('Incoming stream has started', streamSid);
                            break;
                        default:
                            console.log('Received non-media event:', data.event);
                            break;
                    }
                } catch (error) {
                    console.error('Error parsing message:', error, 'Message:', message);
                }
            });
            // Handle connection close
            connection.on('close', () => {
                if (openAiWs.ws.readyState === WebSocket.OPEN) openAiWs.close();
                console.log('Client disconnected.');
            });
            
            openAiWs.onClose();
            openAiWs.onError();
        });
    });


    fastify.listen({ port: PORT, host: "0.0.0.0" }, (err) => {
        if (err) {
            console.error(err);
            process.exit(1);
        }
        console.log(`Server is listening on port ${PORT}`);
    });
}
catch(err){
    console.log(err);
    
}