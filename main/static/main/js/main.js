const app = new Vue({
  el: "#app",
  delimiters: ['${', '}'],
  data: {
    results: null,
  },
  computed: {
    pulledResults: function() {
      return this.results && typeof this.results['total_fr'] !== 'undefined';
    },
  },
  mounted: function() {
    this.results = JSON.parse(document.getElementById('results').textContent);
    console.log(this.results);
  },
});