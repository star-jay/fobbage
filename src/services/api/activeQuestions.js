import Resource from '@/services/resource';
import client from './fobbageClient';

export default new Resource(client, 'api/active_fobbits');
