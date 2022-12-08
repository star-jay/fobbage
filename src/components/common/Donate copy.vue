<template>
  <div id="paypal-button-container"></div>
</template>
<!-- <script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="reinjanef" data-color="#40DCA5" data-emoji="🐟"  data-font="Poppins" data-text="Buy my fish some fishfood" data-outline-color="#000000" data-font-color="#ffffff" data-coffee-color="#FFDD00" ></script> -->

<script>
import { loadScript } from '@paypal/paypal-js';

// https://www.paypal.com/donate/?business=9FRP6E9BJUV3J&no_recurring=1&item_name=Thanks+for+helping+me+buy+fish+food%21&currency_code=EUR

export default {
  name: 'Donate',
  components: {
  },
  async mounted() {
    const paypalSdk = await loadScript({
      'client-id': '9FRP6E9BJUV3J',
      currency: 'EUR',
    });
    paypalSdk.Buttons().render('#paypal-button-container');
  },
};
</script>
