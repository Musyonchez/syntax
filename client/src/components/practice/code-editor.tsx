"use client"

import { useEffect, useRef, useState } from 'react'
import { EditorView, keymap, highlightSpecialChars, drawSelection } from '@codemirror/view'
import { Extension, EditorState } from '@codemirror/state'
import { foldGutter, indentOnInput, indentUnit, bracketMatching, foldKeymap, syntaxHighlighting, defaultHighlightStyle } from '@codemirror/language'
import { history, defaultKeymap, historyKeymap } from '@codemirror/commands'
import { searchKeymap } from '@codemirror/search'
import { autocompletion, completionKeymap, closeBrackets, closeBracketsKeymap } from '@codemirror/autocomplete'
import { lintKeymap } from '@codemirror/lint'
import { python } from '@codemirror/lang-python'
import { javascript } from '@codemirror/lang-javascript'
import { oneDark } from '@codemirror/theme-one-dark'
import { useTheme } from 'next-themes'

interface CodeEditorProps {
  value: string
  onChange: (value: string) => void
  language: 'python' | 'javascript'
  readOnly?: boolean
  placeholder?: string
  className?: string
}

export function CodeEditor({
  value,
  onChange,
  language,
  readOnly = false,
  placeholder = "Enter your code...",
  className = ""
}: CodeEditorProps) {
  const editor = useRef<HTMLDivElement>(null)
  const view = useRef<EditorView | null>(null)
  const { theme } = useTheme()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    if (!editor.current || !mounted) return

    // Language extension
    const languageExtension = language === 'python' ? python() : javascript()
    
    // Theme extension
    const themeExtension = theme === 'dark' ? oneDark : []
    
    // Basic setup extensions
    const basicExtensions = [
      highlightSpecialChars(),
      history(),
      foldGutter(),
      drawSelection(),
      indentUnit.of("  "),
      EditorState.allowMultipleSelections.of(true),
      indentOnInput(),
      bracketMatching(),
      closeBrackets(),
      autocompletion(),
      syntaxHighlighting(defaultHighlightStyle, { fallback: true }),
      keymap.of([
        ...closeBracketsKeymap,
        ...defaultKeymap,
        ...searchKeymap,
        ...historyKeymap,
        ...foldKeymap,
        ...completionKeymap,
        ...lintKeymap
      ])
    ]

    // Extensions
    const extensions: Extension[] = [
      ...basicExtensions,
      languageExtension,
      themeExtension,
      EditorView.updateListener.of((update) => {
        if (update.docChanged && !readOnly) {
          onChangeRef.current(update.state.doc.toString())
        }
      }),
      EditorState.readOnly.of(readOnly),
      EditorView.theme({
        '&': {
          fontSize: '14px',
          fontFamily: 'var(--font-mono)',
        },
        '.cm-content': {
          padding: '12px',
          minHeight: '200px',
        },
        '.cm-focused': {
          outline: 'none',
        },
        '.cm-editor': {
          borderRadius: '8px',
          border: theme === 'dark' 
            ? '1px solid hsl(var(--border))' 
            : '1px solid hsl(var(--border))',
        },
        '.cm-scroller': {
          fontFamily: 'var(--font-mono)',
        },
      })
    ]

    // Create editor state
    const state = EditorState.create({
      doc: value,
      extensions,
    })

    // Create editor view
    view.current = new EditorView({
      state,
      parent: editor.current,
    })

    return () => {
      if (view.current) {
        view.current.destroy()
        view.current = null
      }
    }
  }, [mounted, theme, language, readOnly, value])

  // Update content when value changes externally
  useEffect(() => {
    if (view.current && value !== view.current.state.doc.toString()) {
      view.current.dispatch({
        changes: {
          from: 0,
          to: view.current.state.doc.length,
          insert: value,
        },
      })
    }
  }, [value])

  // Store onChange in ref to avoid dependency issues
  const onChangeRef = useRef(onChange)
  onChangeRef.current = onChange

  if (!mounted) {
    return (
      <div className={`rounded-md border bg-muted p-3 ${className}`}>
        <div className="text-sm text-muted-foreground">Loading editor...</div>
      </div>
    )
  }

  return (
    <div className={`relative ${className}`}>
      <div ref={editor} className="min-h-[200px]" />
      {placeholder && !value && (
        <div className="absolute top-3 left-3 text-sm text-muted-foreground pointer-events-none">
          {placeholder}
        </div>
      )}
    </div>
  )
}