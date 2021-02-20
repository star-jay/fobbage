import Resource from '@/services/resource';
import client from './fobbageClient';

export default new Resource(client, 'api/sessions',
  {
    nextQuestion(id) {
      const url = `/${this.base}/${id}/next_question/`;
      return this.client.post(url);
    },
    setActiveFobbit(id, fobbit) {
      const url = `/${this.base}/${id}/set_active_fobbit/`;
      return this.client.post(url, { active_fobbit: fobbit.id });
    },
    join(id) {
      const url = `/${this.base}/${id}/join/`;
      return this.client.post(url);
    },
  });
