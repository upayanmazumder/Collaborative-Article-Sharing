const ENV = process.env.NEXT_PUBLIC_ENV;

export const NEXT_PUBLIC_API_URL = ENV === 'development' ? 'http://localhost:4000' : 'https://api.cas.upayan.dev';