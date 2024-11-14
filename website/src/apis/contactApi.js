import emailjs from '@emailjs/browser';

const phishingApi = {
  serviceId: import.meta.env.PD_SEVICE_ID,
  templateId: import.meta.env.PD_TEMPLATE_ID,
  publicKey: import.meta.env.PD_PUBLIC_KEY,

  send(data) {
    return emailjs.send(this.serviceId, this.templateId, data, {
      publicKey: this.publicKey,
    });
  },
};

export default phishingApi;
