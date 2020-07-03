/**
 * Resource class
 */

import axios from '@/utils/axiosClient';

class Resource {
  constructor(base, otherActions) {
    this.base = base;
    Object.assign(this, otherActions);
  }

  get(id, options) {
    let axiosOptions = options;
    let url = `/${this.base}/`;
    // If only an object is passed, those will be options
    if (typeof id === 'object') {
      axiosOptions = id;
    // Anything else will be the id of the resource
    } else if (id !== undefined) {
      url += `${id}/`;
    }
    return axios.get(url, axiosOptions);
  }

  delete(id, options) {
    const url = `/${this.base}/${id}/`;
    return axios.delete(url, options);
  }

  post(options) {
    const url = `/${this.base}/`;
    return axios.post(url, options);
  }

  put(id, options) {
    const url = `/${this.base}/${id}/`;
    return axios.put(url, options);
  }

  patch(id, options) {
    const url = `/${this.base}/${id}/`;
    return axios.patch(url, options);
  }
}

export default Resource;
