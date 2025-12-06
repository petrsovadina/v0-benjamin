"use client"

import type React from "react"
import { useState } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { createClient } from "@/lib/supabase/client"

export function ResetPasswordForm() {
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")
  const [passwordMatch, setPasswordMatch] = useState(true)
  const router = useRouter()
  const searchParams = useSearchParams()

  const handlePasswordChange = (value: string) => {
    setPassword(value)
    setPasswordMatch(value === confirmPassword)
  }

  const handleConfirmPasswordChange = (value: string) => {
    setConfirmPassword(value)
    setPasswordMatch(value === password)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    if (!passwordMatch) {
      setError("Hesla se neshodují")
      return
    }

    setIsLoading(true)

    try {
      const supabase = createClient()

      const { error } = await supabase.auth.updateUser({
        password,
      })

      if (error) {
        setError(error.message)
      } else {
        router.push("/auth/login?reset=success")
      }
    } catch (err) {
      setError("Nepodařilo se obnovit heslo. Zkuste to znovu.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card className="p-6 border border-border bg-card">
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Password field */}
        <div className="space-y-2">
          <label htmlFor="password" className="text-sm font-medium text-foreground">
            Nové heslo
          </label>
          <Input
            id="password"
            type="password"
            placeholder="Minimálně 8 znaků"
            value={password}
            onChange={(e) => handlePasswordChange(e.target.value)}
            required
            minLength={8}
            className="bg-input border-border text-foreground placeholder:text-muted-foreground"
          />
          <p className="text-xs text-muted-foreground">Minimálně 8 znaků</p>
        </div>

        {/* Confirm password field */}
        <div className="space-y-2">
          <label htmlFor="confirmPassword" className="text-sm font-medium text-foreground">
            Potvrdit heslo
          </label>
          <Input
            id="confirmPassword"
            type="password"
            placeholder="Zopakujte heslo"
            value={confirmPassword}
            onChange={(e) => handleConfirmPasswordChange(e.target.value)}
            required
            className={`bg-input border text-foreground placeholder:text-muted-foreground ${
              !passwordMatch ? "border-destructive" : "border-border"
            }`}
          />
          {!passwordMatch && <p className="text-xs text-destructive">Hesla se neshodují</p>}
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
          disabled={isLoading || !passwordMatch || !password}
          className="w-full bg-primary text-primary-foreground hover:bg-primary/90"
        >
          {isLoading ? "Obnovuji heslo..." : "Obnovit heslo"}
        </Button>
      </form>
    </Card>
  )
}
