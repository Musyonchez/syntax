'use client'

interface ConfirmModalProps {
  title: string
  description: string
  confirmText?: string
  cancelText?: string
  onConfirm: () => void
  onCancel: () => void
  loading?: boolean
  isDestructive?: boolean
}

export function ConfirmModal({
  title,
  description,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  onConfirm,
  onCancel,
  loading = false,
  isDestructive = false
}: ConfirmModalProps) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" role="dialog" aria-modal="true" aria-labelledby="confirm-modal-title" aria-describedby="confirm-modal-description">
      <div className="bg-background border border-border rounded-xl p-6 w-full max-w-md m-4">
        <div className="space-y-4">
          <div className="space-y-2">
            <h2 id="confirm-modal-title" className="text-lg font-semibold text-foreground">
              {title}
            </h2>
            <p id="confirm-modal-description" className="text-sm text-muted-foreground">
              {description}
            </p>
          </div>
          
          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={onCancel}
              disabled={loading}
              className="px-4 py-2 text-foreground border border-border rounded-md hover:bg-foreground/5 transition-colors disabled:opacity-50"
            >
              {cancelText}
            </button>
            <button
              type="button"
              onClick={onConfirm}
              disabled={loading}
              className={`px-4 py-2 rounded-md transition-colors disabled:opacity-50 ${
                isDestructive
                  ? 'bg-red-600 text-white hover:bg-red-700'
                  : 'bg-foreground text-background hover:bg-foreground/90'
              }`}
            >
              {loading ? 'Processing...' : confirmText}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}