import Resource from '@/services/resource';
import client from './fobbageClient';

export default new Resource(client, 'api/simple_token');
