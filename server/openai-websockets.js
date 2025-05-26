export class OpenAIWS{
    constructor(apiKey){       
        this.openAiWs = new WebSocket('wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01', {
            headers: {
                Authorization: `Bearer ${apiKey}`,
                "OpenAI-Beta": "realtime=v1"
            }
        });
    }    
    
    
            
    sendSessionUpdate = () => {
        const sessionUpdate = {
            type: 'session.update',
            session: {
                turn_detection: { type: 'server_vad' },
                input_audio_format: 'g711_ulaw',
                output_audio_format: 'g711_ulaw',
                voice: VOICE,
                instructions: "You are an ai assistant taking place of the voicemail to get userful info from the caller and schedule callbacks",
                modalities: ["text", "audio"],
                temperature: 0.8,
            }
        };
        console.log('Sending session update:', JSON.stringify(sessionUpdate));
        openAiWs.send(JSON.stringify(sessionUpdate));
    }


    onOpen(){   
        openAiWs.on('open', () => {
            console.log('Connected to the OpenAI Realtime API');
            setTimeout(this.sendSessionUpdate, 250); // Ensure connection stability, send after .25 seconds
        });
        
    }

    onMsg(connection){
        openAiWs.on('message', (data) => {
                try {
                    const response = JSON.parse(data);
                    console.log(response.type);
                    
                    if (LOG_EVENT_TYPES.includes(response.type)) {
                        console.log(`Received event: ${response.type}`, response);
                    }
                    if (response.type === 'session.updated') {
                        console.log('Session updated successfully:', response);
                    }
                    if (response.type === 'response.audio.delta' && response.delta) {
                        const audioDelta = {
                            event: 'media',
                            streamSid: streamSid,
                            media: { payload: Buffer.from(response.delta, 'base64').toString('base64') }
                        };
                        connection.send(JSON.stringify(audioDelta));
                    }
                } catch (error) {
                    console.error('Error processing OpenAI message:', error, 'Raw message:', data);
                }
            });
            
        }

    onClose(){
        this.ws.on('close', () => {
            console.log('Disconnected from the OpenAI Realtime API');
        });
    }

    onError(){
        this.ws.on('error', (error) => {
                console.error('Error in the OpenAI WebSocket:', error);
            });
    }

    send(data){
        this.ws.send(data)
    }


}