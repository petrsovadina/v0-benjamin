import { createClient } from '@supabase/supabase-js';
import { NextResponse } from 'next/server';

// Initialize Supabase client
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const supabase = createClient(supabaseUrl, supabaseKey);

export async function POST(req: Request) {
    try {
        const json = await req.json();
        const { message, messages } = json;

        // Validate Auth
        // Using middleware for primary protection, but good to have user ID here
        // Proxy to Python Backend
        const backendUrl = `${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'}/api/v1/query`;

        const response = await fetch(backendUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message || messages?.[messages.length - 1]?.content,
                history: messages || []
            }),
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error("Backend Error:", errorText);
            return NextResponse.json({ error: `Backend Error: ${response.statusText}` }, { status: response.status });
        }

        const data = await response.json();
        return NextResponse.json({
            role: 'assistant',
            content: data.response,
            metadata: data.metadata
        });

    } catch (error: any) {
        console.error('API Error:', error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
