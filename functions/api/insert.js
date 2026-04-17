export async function onRequestPost(context) {
  const { request, env } = context;
  
  // 簡易認証: API_SECRET_KEY ヘッダーをチェック
  const authHeader = request.headers.get("X-API-SECRET-KEY");
  if (authHeader !== env.API_SECRET_KEY) {
    return new Response("Unauthorized", { status: 401 });
  }

  try {
    const data = await request.json();
    const { ticker, date, open, high, low, close, volume } = data;

    await env.DB.prepare(
      "INSERT OR REPLACE INTO stocks (ticker, date, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?, ?)"
    )
      .bind(ticker, date, open, high, low, close, volume)
      .run();

    return new Response(JSON.stringify({ success: true }), {
      headers: { "Content-Type": "application/json" },
    });
  } catch (err) {
    return new Response(err.message, { status: 500 });
  }
}
