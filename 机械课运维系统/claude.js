#!/usr/bin/env node

require('dotenv').config();
const Anthropic = require('@anthropic-ai/sdk');
const readline = require('readline');

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

async function chatWithClaude() {
  try {
    console.log('欢迎使用 Claude 聊天！输入 "exit" 退出。\n');
    
    while (true) {
      const userInput = await new Promise(resolve => {
        rl.question('你: ', resolve);
      });

      if (userInput.toLowerCase() === 'exit') {
        console.log('再见！');
        rl.close();
        break;
      }

      const message = await anthropic.messages.create({
        model: "claude-3-opus-20240229",
        max_tokens: 1024,
        messages: [
          {
            role: "user",
            content: userInput
          }
        ]
      });

      console.log('\nClaude:', message.content[0].text, '\n');
    }
  } catch (error) {
    console.error('发生错误：', error);
    rl.close();
  }
}

chatWithClaude(); 