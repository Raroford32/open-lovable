import { appConfig } from '@/config/app.config';
import { createOpenAI } from '@ai-sdk/openai';
type ProviderName = 'openrouter';

// Client function type returned by @ai-sdk providers
export type ProviderClient =
  | ReturnType<typeof createOpenAI>;

export interface ProviderResolution {
  client: ProviderClient;
  actualModel: string;
}

// Cache provider clients by a stable key to avoid recreating
const clientCache = new Map<string, ProviderClient>();

function getEnvDefaults(provider: ProviderName): { apiKey?: string; baseURL?: string } {
  switch (provider) {
    case 'openrouter':
      return { apiKey: process.env.OPENROUTER_API_KEY, baseURL: process.env.OPENROUTER_BASE_URL || 'https://openrouter.ai/api/v1' };
    default:
      return {};
  }
}

function getOrCreateClient(provider: ProviderName, apiKey?: string, baseURL?: string): ProviderClient {
  const effective = { apiKey, baseURL };

  const cacheKey = `${provider}:${effective.apiKey || ''}:${effective.baseURL || ''}`;
  const cached = clientCache.get(cacheKey);
  if (cached) return cached;

  let client: ProviderClient;
  switch (provider) {
    case 'openrouter':
      client = createOpenAI({ apiKey: effective.apiKey || getEnvDefaults('openrouter').apiKey, baseURL: effective.baseURL ?? getEnvDefaults('openrouter').baseURL });
      break;
    default:
      client = createOpenAI({ apiKey: effective.apiKey || getEnvDefaults('openrouter').apiKey, baseURL: effective.baseURL ?? getEnvDefaults('openrouter').baseURL });
  }

  clientCache.set(cacheKey, client);
  return client;
}

export function getProviderForModel(modelId: string): ProviderResolution {
  // 1) Check explicit model configuration in app config (custom models)
  const configured = appConfig.ai.modelApiConfig?.[modelId as keyof typeof appConfig.ai.modelApiConfig];
  if (configured) {
    const { provider, apiKey, baseURL, model } = configured as { provider: ProviderName; apiKey?: string; baseURL?: string; model: string };
    const client = getOrCreateClient(provider, apiKey, baseURL);
    return { client, actualModel: model };
  }

  // 2) Fallback logic based on prefixes and special cases
  const isOpenRouter = modelId.startsWith('openrouter/');
  const client = getOrCreateClient('openrouter');
  return { client, actualModel: isOpenRouter ? modelId.replace('openrouter/', '') : modelId };
}

export default getProviderForModel;


