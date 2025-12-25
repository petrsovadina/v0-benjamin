'use client';

import { useReportWebVitals } from 'next/web-vitals';

export function WebVitals() {
    useReportWebVitals((metric) => {
        // Pro MVP logujeme do konzole. V produkci bychom posílali např. na Vercel Analytics nebo vlastní endpoint.
        console.log('[Web Vitals]', metric);
    });

    return null;
}
