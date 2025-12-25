"use client"

import React, { Component, ErrorInfo, ReactNode } from "react"
import { AlertCircle, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"

interface Props {
    children?: ReactNode
    fallback?: ReactNode
}

interface State {
    hasError: boolean
    error: Error | null
}

export class ErrorBoundary extends Component<Props, State> {
    public state: State = {
        hasError: false,
        error: null,
    }

    public static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error }
    }

    public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        console.error("Uncaught error:", error, errorInfo)
    }

    public render() {
        if (this.state.hasError) {
            if (this.props.fallback) {
                return this.props.fallback
            }

            return (
                <Alert variant="destructive" className="my-4">
                    <AlertCircle className="h-4 w-4" />
                    <AlertTitle>Something went wrong</AlertTitle>
                    <AlertDescription className="mt-2 flex flex-col gap-2">
                        <p>An unexpected error occurred in the application interface.</p>
                        {this.state.error && (
                            <pre className="text-xs bg-black/10 p-2 rounded overflow-auto max-h-20">
                                {this.state.error.message}
                            </pre>
                        )}
                        <Button
                            variant="outline"
                            size="sm"
                            className="w-fit mt-2"
                            onClick={() => this.setState({ hasError: false, error: null })}
                        >
                            <RefreshCw className="mr-2 h-3 w-3" />
                            Try again
                        </Button>
                    </AlertDescription>
                </Alert>
            )
        }

        return this.props.children
    }
}
