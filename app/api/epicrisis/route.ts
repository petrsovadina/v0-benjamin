import { NextResponse } from 'next/server';

export async function POST(req: Request) {
    try {
        const json = await req.json();
        const { items } = json;

        const backendUrl = `${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'}/api/v1/ai/epicrisis`;

        const response = await fetch(backendUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ items }),
        });

        if (!response.ok) {
            return NextResponse.json({ error: `Backend Error: ${response.statusText}` }, { status: response.status });
        }

        const data = await response.json();
        return NextResponse.json(data);

    } catch (error: any) {
        console.error('API Error:', error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
