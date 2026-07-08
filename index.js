// ... standard imports ...

async function main() {
    console.clear();
    logger.banner();

    const host = await ask(' Target Hostname/IP: ');
    const port = await ask(' Target Port: ');
    const protocolType = await ask(' Protocol Mode (1 = Java, 2 = Bedrock, 3 = Hybrid): ');
    const maxCount = parseInt(await ask(' Total Concurrent Instances: '));
    const delay = parseInt(await ask(' Connection Throttle Interval (ms): '));

    const config = {
        host,
        port,
        autoReconnect: true,
        reconnectDelay: 5000,
        version: false
    };

    const java = new JavaEngine(config);
    const bedrock = new BedrockEngine(config);

    logger.info(`OP INJOY Matrix initializing... Max instances: ${maxCount}`);

    for (let i = 0; i < maxCount; i++) {
        const baseIdentity = generator.generateString(8);
        
        if (protocolType === '1' || protocolType === '3') {
            java.spawn(`INJOY_${baseIdentity}_JV`);
        }
        if (protocolType === '2' || protocolType === '3') {
            bedrock.spawn(`INJOY_${baseIdentity}_BR`);
        }

        await new Promise(res => setTimeout(res, delay));
    }
}
// ... rest of the execution logic ...
