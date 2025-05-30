const getTwimlResponse = (RerouteResponse, request) => {
    return `<?xml version="1.0" encoding="UTF-8"?>
        <Response>
        <Say>${RerouteResponse}</Say>
        <Pause length="1"/>
        <Say>Say hello to begin conversation!</Say>
        <Connect>
        <Stream url="wss://${request.headers.host}/media-stream" />
        </Connect>
        </Response>`;
}


const sendSessionUpdate = (openAiWs) => {
    const SYSTEM_MESSAGE = 'You are a helpful AI phone assistant for me. Callers can either pass a message along or schedule a callback where they provide a date for me to call them back most convneient for them. And always be sure to ask whos calling. ';
    const VOICE = 'alloy';
    const sessionUpdate = {

        type: 'session.update',
        session: {
            turn_detection: { type: 'server_vad' },
            input_audio_format: 'g711_ulaw',
            output_audio_format: 'g711_ulaw',
            voice: VOICE,
            instructions: SYSTEM_MESSAGE,
            modalities: ["text", "audio"],
            temperature: 0.8,
            input_audio_transcription: {
                model: "gpt-4o-transcribe",
            },
        },
    };
    openAiWs.send(JSON.stringify(sessionUpdate));
};



export { getTwimlResponse, sendSessionUpdate }