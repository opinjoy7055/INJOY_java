const mineflayer = require('mineflayer');
let bedrock;
try { bedrock = require('bedrock-protocol'); } catch(e){}

// --- Auto IP & Port Parsing ---
const targetInput = process.env.TARGET_IP || '127.0.0.1';
const [host, portStr] = targetInput.split(':');
const javaPort = portStr ? parseInt(portStr) : 25565;
const bedrockPort = portStr ? parseInt(portStr) : 19132;

// --- Configs ---
const botCount = parseInt(process.env.BOT_COUNT) || 10;
const edition = process.env.EDITION || '3'; 
const speed = process.env.SPEED || '1';
const afkMode = process.env.AFK_MODE || '1';
const spamMsg = process.env.SPAM_MSG || '';
const followTarget = process.env.FOLLOW_TARGET || '';

// --- V4 Custom Name / Password Logic ---
const customName = process.env.BOT_NAME || '';
const userPassword = process.env.BOT_PASSWORD;
const aiPassword = userPassword ? userPassword : `InjoyV4@${Math.floor(1000 + Math.random() * 9000)}`;

const joinDelay = speed === '3' ? 2000 : 6000;
let currentBot = 1;

function getBaseName(index) {
    if (customName) return botCount > 1 ? `${customName}_${index}` : customName;
    return `INJOY_${Math.random().toString(36).substring(2, 6).toUpperCase()}_${Math.floor(100 + Math.random() * 900)}`;
}

function spawnJava(username) {
    console.log(`[Java] Deploying: ${username}`);
    const bot = mineflayer.createBot({ host, port: javaPort, username, version: '1.21.4', physicsEnabled: true });
    
    bot.once('spawn', () => {
        console.log(`[Java] Online: ${username}`);
        setTimeout(() => bot.chat(`/register ${aiPassword} ${aiPassword}`), 2000);
        setTimeout(() => bot.chat(`/login ${aiPassword}`), 3000);
        
        if (afkMode === '1') {
            setInterval(() => { try { bot.setControlState('forward', true); setTimeout(() => bot.setControlState('forward', false), 2000); bot.look(Math.random() * Math.PI * 2, 0); } catch(e){} }, 4000);
        } else if (afkMode === '2') {
            setInterval(() => { try { bot.setControlState('jump', true); bot.setControlState('sneak', true); setTimeout(() => { bot.setControlState('jump', false); bot.setControlState('sneak', false); }, 1000); } catch(e){} }, 2000);
        } else if (afkMode === '3' && followTarget) { // Follow Player Tracking
            setInterval(() => { 
                try {
                    const targetEntity = bot.players[followTarget]?.entity;
                    if (targetEntity) {
                        bot.lookAt(targetEntity.position.offset(0, targetEntity.height, 0));
                        bot.setControlState('forward', bot.entity.position.distanceTo(targetEntity.position) > 2);
                    } else {
                        bot.setControlState('forward', false);
                    }
                } catch(e){} 
            }, 500);
        }

        if (spamMsg) {
            setInterval(() => { try { bot.chat(`${spamMsg} [${Math.floor(Math.random()*1000)}]`); } catch(e){} }, 4000);
        }
    });

    bot.on('error', () => {});
    // Important: Reconnects using the exact same username to keep items!
    bot.on('kicked', () => setTimeout(() => spawnJava(username), joinDelay));
}

function spawnBedrock(username) {
    if (!bedrock) return;
    console.log(`[Bedrock] Deploying: ${username}`);
    try {
        const client = bedrock.createClient({ host, port: bedrockPort, username, version: '1.26.30', offline: true });
        client.on('join', () => console.log(`[Bedrock] Online: ${username}`));
        client.on('disconnect', () => setTimeout(() => spawnBedrock(username), joinDelay));
        client.on('error', () => {});
    } catch (e) {}
}

function deploySwarm() {
    if (currentBot > botCount) {
        console.log('[Engine] All bots deployed.');
        return;
    }
    const base = getBaseName(currentBot);
    
    // Auto-formatting names so they fit Bedrock/Java requirements
    if (edition === '1') spawnJava(base);
    else if (edition === '2') spawnBedrock(base);
    else if (edition === '3') {
        spawnJava(`${base}_J`);
        spawnBedrock(`${base}_B`);
    }
    
    currentBot++;
    setTimeout(deploySwarm, joinDelay);
}

deploySwarm();
