require('dotenv').config();
const Anthropic = require('@anthropic-ai/sdk');

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

async function main() {
  try {
    const message = await anthropic.messages.create({
      model: "claude-3-opus-20240229",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: "你好，请介绍一下你自己"
        }
      ]
    });
    console.log('Claude 的回复：', message.content[0].text);
  } catch (error) {
    console.error('发生错误：', error);
  }
}

main(); 