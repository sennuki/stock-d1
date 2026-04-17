export async function onRequestGet(context) {
  const { env } = context;
  
  try {
    const { results } = await env.DB.prepare(
      "SELECT * FROM stocks WHERE ticker = 'AAPL' ORDER BY date DESC LIMIT 30"
    ).all();

    return new Response(JSON.stringify(results), {
      headers: { "Content-Type": "application/json" },
    });
  } catch (err) {
    return new Response(err.message, { status: 500 });
  }
}
