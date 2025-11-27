import Link, { LinkProps } from "next/link"
import React from "react"

interface CustomLinkProps extends LinkProps {
    children: React.ReactNode
    className?: string
    external?: boolean
    variant?:
        | "default"
        | "nav"
        | "button"
        | "underline"
        | "primary"
        | "secondary"
    target?: string
    rel?: string
}

export default function CustomLink({
    children,
    className = "",
    external = false,
    variant = "default",
    ...props
}: CustomLinkProps) {
    const variants = {
        default: "text-primary-600 hover:text-primary-700 transition-colors",
        primary: "text-primary-600 hover:text-primary-700 transition-colors",
        secondary: "text-gray-600 hover:text-gray-900 transition-colors",
        nav: "text-gray-600 hover:text-primary-600 transition-colors font-semibold",
        button: "", // Usually used with Button component inside or styling passed via className
        underline:
            "text-primary-600 hover:text-primary-700 hover:underline transition-all"
    }

    if (external) {
        return (
            <a
                href={props.href.toString()}
                className={`${variants[variant]} ${className}`}
                target='_blank'
                rel='noopener noreferrer'>
                {children}
            </a>
        )
    }

    return (
        <Link {...props} className={`${variants[variant]} ${className}`}>
            {children}
        </Link>
    )
}
