"use client"; 

import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("");

  const handleSend = async () => {
    const res = await axios.post("http://127.0.0.1:8000/chat", { "message": message });
    console.log(res.data);
    setReply(res.data.response.message.blocks[0].text);
  };

  return (
    <main className="min-h-screen p-10 bg-gray-50">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold mb-4">💬 AI Chat Assistant</h1>
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="输入你的问题..."
          className="w-full p-4 rounded border"
          rows={5}
        />
        <button
          onClick={handleSend}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded"
        >
          发送
        </button>

        {reply && (
          <div className="mt-6 bg-white p-4 rounded shadow">
            <strong>AI 回复：</strong>
            <p className="mt-2 whitespace-pre-wrap">{reply}</p>
          </div>
        )}
      </div>
    </main>
  );
}
