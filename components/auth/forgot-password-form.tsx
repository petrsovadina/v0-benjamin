"use client"

import type React from "react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { createClient } from "@/lib/supabase/client"

export function ForgotPasswordForm() {
  const [email, setEmail] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")
  const [success, setSuccess] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setSuccess(false)
    setIsLoading(true)

    try {
      const supabase = createClient()

      const { error } = await supabase.auth.resetPasswordForEmail(email, {
        redirectTo: `${window.location.origin}/auth/reset-password`,
      })

      if (error) {
        setError(error.message)
      } else {
        setSuccess(true)
        setEmail("")
      }
    } catch (err) {
      setError("Nepodařilo se odeslat email. Zkuste to znovu.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card className="p-6 border border-border bg-card">
      {success && (
        <div className="p-3 rounded-md bg-green-500/10 border border-green-500/20 text-green-600 dark:text-green-400 text-sm mb-4">
          Email pro obnovení hesla byl odeslán. Zkontrolujte si inbox.
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Email field */}
        <div className="space-y-2">
          <label htmlFor="email" className="text-sm font-medium text-foreground">
            Email
          </label>
          <Input
            id="email"
            type="email"
            placeholder="vas@email.cz"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="bg-input border-border text-foreground placeholder:text-muted-foreground"
          />
        </div>

        {/* Error message */}
        {error && (
          <div className="p-3 rounded-md bg-destructive/10 border border-destructive/20 text-destructive text-sm">
            {error}
          </div>
        )}

        {/* Submit button */}
        <Button
          type="submit"
          disabled={isLoading || !email}
          className="w-full bg-primary text-primary-foreground hover:bg-primary/90"
        >
          {isLoading ? "Odesílám..." : "Odeslat reset email"}
        </Button>
      </form>
    </Card>
  )
}
