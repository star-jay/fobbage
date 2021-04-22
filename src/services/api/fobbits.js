import Resource from '@/services/resource';
import client from './fobbageClient';

export default new Resource(client, 'api/fobbits',
  {
    generateAnswers(id) {
      const url = `/${this.base}/${id}/generate_answers/`;
      return this.client.post(url);
    },
    finish(id, options) {
      const url = `/${this.base}/${id}/finish/`;
      return this.client.post(url, options);
    },
    reset(id) {
      const url = `/${this.base}/${id}/reset/`;
      return this.client.post(url);
    },
  });
