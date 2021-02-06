import Resource from '@/services/resource';
import client from './fobbageClient';

export default new Resource(client, 'api/sessions',
  {
    nextQuestion(id) {
      const url = `/${this.base}/${id}/next_question/`;
      return this.client.post(url);
    },
  });
