import Resource from '@/services/resource';
import { client } from './authClient';

export default new Resource(client, 'users');
