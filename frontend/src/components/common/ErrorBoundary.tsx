import { Component, type ErrorInfo, type ReactNode } from 'react';

interface Props {
  children?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-slate-50 p-4">
          <div className="max-w-md w-full bg-white p-8 rounded-3xl shadow-xl border border-slate-100 text-center space-y-6">
            <div className="w-16 h-16 bg-rose-50 text-rose-500 rounded-full flex items-center justify-center mx-auto">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/>
                <path d="M12 9v4"/><path d="M12 17h.01"/>
              </svg>
            </div>
            <div>
              <h2 className="text-2xl font-bold text-slate-900">Something went wrong</h2>
              <p className="text-slate-500 mt-2">
                An unexpected error occurred. We've been notified and are working on it.
              </p>
            </div>
            <button
              onClick={() => window.location.reload()}
              className="flex items-center justify-center gap-2 w-full py-3 px-4 bg-blue-600 text-white font-medium rounded-xl hover:bg-blue-700 transition-all"
            >
              ↻ Reload Application
            </button>
            <div className="pt-4 text-xs text-slate-400 font-mono overflow-hidden text-ellipsis whitespace-nowrap">
              {this.state.error?.message}
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
