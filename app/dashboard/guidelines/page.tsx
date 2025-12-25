'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Upload, FileText, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';

export default function GuidelinesUploadPage() {
    const [file, setFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');
    const [message, setMessage] = useState('');

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
            setStatus('idle');
            setMessage('');
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setUploading(true);
        setStatus('idle');

        const formData = new FormData();
        formData.append('file', file);

        try {
            // Assuming Next.js rewrites /api/v1 -> Backend URL
            const response = await fetch('/api/v1/admin/upload/guideline', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`);
            }

            const result = await response.json();
            setStatus('success');
            setMessage(`Soubor ${result.filename} byl úspěšně nahrán a zpracovává se.`);
            setFile(null);
        } catch (error) {
            console.error(error);
            setStatus('error');
            setMessage('Nahrávání selhalo. Zkontrolujte připojení nebo zkuste jiný soubor.');
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="container mx-auto py-8 max-w-2xl">
            <Card>
                <CardHeader>
                    <CardTitle>Nahrát klinický doporučený postup</CardTitle>
                    <CardDescription>
                        Nahrajte PDF soubor s doporučeným postupem. Systém jej automaticky zpracuje, rozdělí a uloží do znalostní báze pro AI.
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">

                    <div className="border-2 border-dashed rounded-lg p-10 flex flex-col items-center justify-center text-center space-y-4 hover:bg-slate-50 transition-colors">
                        <div className="bg-blue-100 p-4 rounded-full">
                            <Upload className="w-8 h-8 text-blue-600" />
                        </div>
                        <div>
                            <p className="text-sm font-medium">Klikněte pro výběr nebo přetáhněte soubor sem</p>
                            <p className="text-xs text-muted-foreground mt-1">Podporováno: PDF (max 50MB)</p>
                        </div>
                        <input
                            type="file"
                            accept=".pdf"
                            onChange={handleFileChange}
                            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                        />
                    </div>

                    {file && (
                        <div className="flex items-center p-4 bg-slate-50 rounded-md border">
                            <FileText className="w-8 h-8 text-blue-500 mr-3" />
                            <div className="flex-1 overflow-hidden">
                                <p className="text-sm font-medium truncate">{file.name}</p>
                                <p className="text-xs text-muted-foreground">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                            </div>
                            <Button
                                onClick={handleUpload}
                                disabled={uploading}
                            >
                                {uploading ? (
                                    <>
                                        <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Nahrávám...
                                    </>
                                ) : (
                                    'Nahrát do báze'
                                )}
                            </Button>
                        </div>
                    )}

                    {status === 'success' && (
                        <Alert variant="default" className="border-green-500 text-green-700 bg-green-50">
                            <CheckCircle className="h-4 w-4" />
                            <AlertTitle>Úspěch</AlertTitle>
                            <AlertDescription>{message}</AlertDescription>
                        </Alert>
                    )}

                    {status === 'error' && (
                        <Alert variant="destructive">
                            <AlertCircle className="h-4 w-4" />
                            <AlertTitle>Chyba</AlertTitle>
                            <AlertDescription>{message}</AlertDescription>
                        </Alert>
                    )}

                </CardContent>
            </Card>

            <div className="mt-8 text-center text-sm text-muted-foreground">
                <p>Tato data budou dostupná pro RAG vyhledávání v chatu.</p>
            </div>
        </div>
    );
}
