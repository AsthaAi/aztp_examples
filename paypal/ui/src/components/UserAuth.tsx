import React, { useEffect, useState } from 'react';
import { Button, Avatar } from 'flowbite-react';
import { UserCircleIcon } from '@heroicons/react/24/outline';
import { useSearchParams } from 'next/navigation';

interface UserInfo {
  name: string;
  email: string;
  picture?: string;
}

export const UserAuth: React.FC = () => {
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  const [isGoogleLoading, setIsGoogleLoading] = useState(false);
  const [isGithubLoading, setIsGithubLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const searchParams = useSearchParams();

  useEffect(() => {
    // Check for error in URL
    const error = searchParams.get('error');
    if (error) {
      setError(`Authentication failed: ${error}`);
    }

    // Check if user info exists in cookie
    const checkUserInfo = async () => {
      try {
        const response = await fetch('/api/auth/user');
        if (response.ok) {
          const data = await response.json();
          setUserInfo(data);
        }
      } catch (error) {
        console.error('Failed to get user info:', error);
      }
    };

    checkUserInfo();
  }, [searchParams]);

  const handleLogin = async (provider: string) => {
    try {
      if (provider === 'google') {
        setIsGoogleLoading(true);
      } else {
        setIsGithubLoading(true);
      }
      setError(null);

      // Call the backend API to initiate OIDC login
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ provider }),
      });

      const data = await response.json();
      console.log('Data:', data);

      if (!response.ok) {
        throw new Error(data.error || 'Login failed');
      }

      if (data.redirectUrl) {
        // Redirect to the OIDC provider
        window.location.href = data.redirectUrl;
      } else {
        throw new Error('No redirect URL received');
      }
    } catch (error) {
      console.error('Login failed:', error);
      setError(error instanceof Error ? error.message : 'Failed to login');
    } finally {
      setIsGoogleLoading(false);
      setIsGithubLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await fetch('/api/auth/logout', { method: 'POST' });
      setUserInfo(null);
      setError(null);
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  if (!userInfo) {
    return (
      <div className="flex flex-row items-end gap-2">
        <Button
          onClick={() => handleLogin('google')}
          disabled={isGoogleLoading || isGithubLoading}
          className="flex items-center gap-2 bg-white hover:!bg-gray-100 text-gray-700 border border-gray-300 shadow-sm"
        >
          <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
            <path
              fill="#4285F4"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            />
            <path
              fill="#34A853"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path
              fill="#FBBC05"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
            />
            <path
              fill="#EA4335"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
            />
          </svg>
          {isGoogleLoading ? 'Logging in...' : 'Login with Google'}
        </Button>
        <Button
          onClick={() => handleLogin('github')}
          disabled={isGoogleLoading || isGithubLoading}
          className="flex items-center gap-2 bg-gray-900 hover:!bg-gray-700 text-white"
        >
          <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
            <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.17 6.839 9.49.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.604-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.464-1.11-1.464-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836c.85.004 1.705.114 2.504.336 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.167 22 16.418 22 12c0-5.523-4.477-10-10-10z" />
          </svg>
          {isGithubLoading ? 'Logging in...' : 'Login with Github'}
        </Button>
        {error && (
          <span className="text-xs text-red-500">{error}</span>
        )}
      </div>
    );
  }

  return (
    <div className="flex items-center gap-3">
      {userInfo.picture ? (
        <Avatar img={userInfo.picture} rounded />
      ) : (
        <Avatar rounded />
      )}
      <div className="flex flex-col">
        <span className="text-sm font-medium text-gray-900">{userInfo.name}</span>
        <span className="text-xs text-gray-500">{userInfo.email}</span>
      </div>
      <Button
        size="xs"
        color="light"
        onClick={handleLogout}
      >
        Logout
      </Button>
    </div>
  );
}; 