import { useState } from 'react';
import { Send } from 'lucide-react';

interface ComposerProps {
  disabled?: boolean;
  onSend: (content: string) => void;
}

/**
 * Composer provides a text input and send button for composing new
 * chat messages.  It calls the `onSend` callback with the input
 * content when the user presses Enter or clicks the send button.  It
 * respects the `disabled` prop to prevent sending while a message is
 * in flight.
 */
export default function Composer({ disabled = false, onSend }: ComposerProps) {
  const [value, setValue] = useState('');

  const handleSubmit = () => {
    const trimmed = value.trim();
    if (!trimmed) return;
    onSend(trimmed);
    setValue('');
  };

  return (
    <div className="flex items-center gap-2 p-4 border-t border-border bg-panel">
      <input
        type="text"
        className="flex-1 bg-panelLight border border-border rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent text-gray-100 placeholder-gray-500"
        placeholder="What's in your mind?"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
          }
        }}
        disabled={disabled}
      />
      <button
        onClick={handleSubmit}
        disabled={disabled || value.trim().length === 0}
        className="flex items-center justify-center w-10 h-10 bg-primary rounded-full hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Send size={18} className="text-white" />
      </button>
    </div>
  );
}