const mineflayer = require('mineflayer');
let bedrock;
try { bedrock = require('bedrock-protocol'); } catch(e){}

// Read commands sent by main.py
const target = process.env.TARGET_IP || '127.0.0.1';
const parts = target.split(':');
const host = parts[0];
const port = parts[1] ? parseInt(parts[1]) : null;
const botCount = parseInt(process.env.BOT_COUNT) || 10;
const edition = process.env.EDITION || '3'; 
const speed = process.env.SPEED || '1';
const afkMode = process.env.AFK_MODE || '1';
const spamMsg = process.env.SPAM_MSG || '';

const joinDelay = speed === '2' ? 12000 : (speed === '3' ? 2000 : 6000);
let currentBot = 1;

function generateName() {
    return `INJOY_${Math.floor(1000 + Math.random() * 9000)}`;
}

function spawnJava(username) {
    console.log(`[Java] Deploying: ${username}`);
    const bot = mineflayer.createBot({ host, port, username, physicsEnabled: true });
    
    bot.once('spawn', () => {
        console.log(`[Java] Online: ${username}`);
        
        // Anti-AFK
        if (afkMode === '1') {
            setInterval(() => { try { bot.setControlState('forward', true); setTimeout(() => bot.setControlState('forward', false), 2000); bot.look(Math.random() * Math.PI * 2, 0); } catch(e){} }, 4000);
        } else if (afkMode === '2') {
            setInterval(() => { try { bot.setControlState('jump', true); bot.setControlState('sneak', true); setTimeout(() => { bot.setControlState('jump', false); bot.setControlState('sneak', false); }, 1000); } catch(e){} }, 2000);
        }

        // Spam
        if (spamMsg) {
            setInterval(() => { try { bot.chat(`${spamMsg} [${Math.floor(Math.random()*1000)}]`); } catch(e){} }, 4000);
        }
    });

    bot.on('error', () => {});
    bot.on('kicked', () => setTimeout(() => spawnJava(generateName()), joinDelay));
}

function spawnBedrock(username) {
    if (!bedrock) return;
    console.log(`[Bedrock] Deploying: ${username}`);
    try {
        const client = bedrock.createClient({ host, port: port || 19132, username, offline: true });
        client.on('join', () => console.log(`[Bedrock] Online: ${username}`));
        client.on('disconnect', () => setTimeout(() => spawnBedrock(generateName() + "BR"), joinDelay));
        client.on('error', () => {});
    } catch (e) {}
}

function deploySwarm() {
    if (currentBot > botCount) {
        console.log('[Engine] All bots deployed.');
        return;
    }
    const base = generateName();
    if (edition === '1' || edition === '3') spawnJava(`${base}_JV`);
    if (edition === '2' || edition === '3') spawnBedrock(`${base}_BR`);
    
    currentBot++;
    setTimeout(deploySwarm, joinDelay);
}

console.log(`[OP INJOY ENGINE] Target: ${host} | Count: ${botCount}`);
deploySwarm();
