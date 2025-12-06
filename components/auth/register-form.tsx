"use client"

import type React from "react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import { signUp } from "@/lib/auth-actions"

export function RegisterForm() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
    acceptTerms: false,
  })
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")
  const [success, setSuccess] = useState(false)
  const [passwordMatch, setPasswordMatch] = useState(true)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target
    const newValue = type === "checkbox" ? checked : value

    setFormData((prev) => ({
      ...prev,
      [name]: newValue,
    }))

    if (name === "confirmPassword" || name === "password") {
      const pwd = name === "password" ? value : formData.password
      const confirm = name === "confirmPassword" ? value : formData.confirmPassword
      setPasswordMatch(pwd === confirm)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setSuccess(false)

    if (!passwordMatch) {
      setError("Hesla se neshodují")
      return
    }

    if (!formData.acceptTerms) {
      setError("Musíte souhlasit s podmínkami služby")
      return
    }

    setIsLoading(true)

    try {
      const result = await signUp(formData.email, formData.password, formData.name)
      if (result.error) {
        setError(result.error)
      } else {
        setSuccess(true)
        setFormData({ name: "", email: "", password: "", confirmPassword: "", acceptTerms: false })
      }
    } catch (err) {
      setError("Registrace se nezdařila. Zkuste to znovu.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card className="p-6 border border-border bg-card">
      {success && (
        <div className="p-3 rounded-md bg-green-500/10 border border-green-500/20 text-green-600 dark:text-green-400 text-sm mb-4">
          Ověřovací email byl odeslán. Zkontrolujte si svůj inbox.
        </div>
      )}
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Name field */}
        <div className="space-y-2">
          <label htmlFor="name" className="text-sm font-medium text-foreground">
            Jméno a příjmení
          </label>
          <Input
            id="name"
            type="text"
            placeholder="MUDr. Jan Novák"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            className="bg-input border-border text-foreground placeholder:text-muted-foreground"
          />
        </div>

        {/* Email field */}
        <div className="space-y-2">
          <label htmlFor="email" className="text-sm font-medium text-foreground">
            Email
          </label>
          <Input
            id="email"
            type="email"
            placeholder="vas@email.cz"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            className="bg-input border-border text-foreground placeholder:text-muted-foreground"
          />
        </div>

        {/* Password field */}
        <div className="space-y-2">
          <label htmlFor="password" className="text-sm font-medium text-foreground">
            Heslo
          </label>
          <Input
            id="password"
            type="password"
            placeholder="Minimálně 8 znaků"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            minLength={8}
            className="bg-input border-border text-foreground placeholder:text-muted-foreground"
          />
          <p className="text-xs text-muted-foreground">Minimálně 8 znaků, obsahuje čísla a speciální znaky</p>
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
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
            required
            className={`bg-input border text-foreground placeholder:text-muted-foreground ${
              !passwordMatch ? "border-destructive" : "border-border"
            }`}
          />
          {!passwordMatch && <p className="text-xs text-destructive">Hesla se neshodují</p>}
        </div>

        {/* Terms checkbox */}
        <div className="flex items-start gap-2">
          <Checkbox
            id="terms"
            name="acceptTerms"
            checked={formData.acceptTerms}
            onCheckedChange={(checked) => setFormData((prev) => ({ ...prev, acceptTerms: checked as boolean }))}
            className="mt-1"
          />
          <label htmlFor="terms" className="text-xs text-muted-foreground leading-relaxed cursor-pointer">
            Souhlasím s{" "}
            <a href="#" className="text-primary hover:underline">
              podmínkami služby
            </a>{" "}
            a{" "}
            <a href="#" className="text-primary hover:underline">
              zásadami ochrany osobních údajů
            </a>
          </label>
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
          disabled={isLoading || !formData.acceptTerms || !passwordMatch}
          className="w-full bg-primary text-primary-foreground hover:bg-primary/90"
        >
          {isLoading ? "Vytvářím účet..." : "Vytvořit účet"}
        </Button>
      </form>
    </Card>
  )
}
