import React from "react"

type TextVariant = "h1" | "h2" | "h3" | "h4" | "body" | "small" | "caption"
type TextColor = "default" | "muted" | "primary" | "white" | "danger" | "success"
type TextWeight = "normal" | "medium" | "semibold" | "bold"

interface TextProps extends React.HTMLAttributes<HTMLElement> {
    variant?: TextVariant
    color?: TextColor
    weight?: TextWeight
    as?: React.ElementType
}

export default function Text({
    children,
    variant = "body",
    color = "default",
    weight,
    as,
    className = "",
    ...props
}: TextProps) {
    const Component = as || (
        variant === "h1" ? "h1" :
        variant === "h2" ? "h2" :
        variant === "h3" ? "h3" :
        variant === "h4" ? "h4" :
        "p"
    )

    const baseStyles = "transition-colors"
    
    const variants = {
        h1: "text-4xl sm:text-6xl tracking-tight",
        h2: "text-3xl sm:text-4xl tracking-tight",
        h3: "text-2xl sm:text-3xl",
        h4: "text-xl",
        body: "text-base sm:text-lg",
        small: "text-sm",
        caption: "text-xs"
    }

    const colors = {
        default: "text-gray-900",
        muted: "text-gray-600",
        primary: "text-orange-600",
        white: "text-white",
        danger: "text-red-600",
        success: "text-green-600"
    }

    const weights = {
        normal: "font-normal",
        medium: "font-medium",
        semibold: "font-semibold",
        bold: "font-bold"
    }

    // Default weights per variant if not specified
    const defaultWeights: Record<TextVariant, TextWeight> = {
        h1: "bold",
        h2: "bold",
        h3: "bold",
        h4: "bold",
        body: "normal",
        small: "normal",
        caption: "normal"
    }

    const selectedWeight = weight || defaultWeights[variant]

    return (
        <Component
            className={`${baseStyles} ${variants[variant]} ${colors[color]} ${weights[selectedWeight]} ${className}`}
            {...props}
        >
            {children}
        </Component>
    )
}

