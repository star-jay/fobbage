import Resource from '@/services/resource';
import client from './fobbageClient';

export default new Resource(client, 'api/sessions',
  {
    nextQuestion(id) {
      const url = `/${this.base}/${id}/next_question/`;
      return this.client.post(url);
    },
    newRound(id, round) {
      const url = `/${this.base}/${id}/new_round/`;
      return this.client.post(url, round);
    },
    setActiveFobbit(id, options) {
      const url = `/${this.base}/${id}/set_active_fobbit/`;
      return this.client.post(url, options);
    },
    join(id) {
      const url = `/${this.base}/${id}/join/`;
      return this.client.post(url);
    },
    getScoreBoard(id) {
      const url = `/${this.base}/${id}/score_board/`;
      return this.client.get(url);
    },
  });
