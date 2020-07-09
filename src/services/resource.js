/**
 * Resource class
 */

import client from '@/services/api/fobbageClient';

class Resource {
  constructor(base, otherActions) {
    this.base = base;
    Object.assign(this, otherActions);
  }

  get(id, options) {
    let clientOptions = options;
    let url = `/${this.base}/`;
    // If only an object is passed, those will be options
    if (typeof id === 'object') {
      clientOptions = id;
    // Anything else will be the id of the resource
    } else if (id !== undefined) {
      url += `${id}/`;
    }
    return client.get(url, clientOptions);
  }

  delete(id, options) {
    const url = `/${this.base}/${id}/`;
    return client.delete(url, options);
  }

  post(options) {
    const url = `/${this.base}/`;
    return client.post(url, options);
  }

  put(id, options) {
    const url = `/${this.base}/${id}/`;
    return client.put(url, options);
  }

  patch(id, options) {
    const url = `/${this.base}/${id}/`;
    return client.patch(url, options);
  }
}

export default Resource;
