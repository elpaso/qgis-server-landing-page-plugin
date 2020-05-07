<template>
  <div class="card-text">
    <dl class="row">
      <template v-for="(value, entry) in project.metadata">
        <template v-if="entry == 'links'">
          <dt class="col-sm-3" :key="entry">{{ entry }}</dt>
          <dd class="col-sm-9" :key="value">
            <ul v-for="item in value" :key="item">
              <li>
                <a :href="item.url">{{ item.name }}</a>
                &mdash; {{ item.description }}
              </li>
            </ul>
          </dd>
        </template>
        <template v-else-if="entry == 'categories' || entry == 'history'">
          <dt class="col-sm-3" :key="entry">{{ entry|camelTitle }}</dt>
          <dd class="col-sm-9" :key="value">
            <ul v-for="item in value" :key="item">
              <li :key="item">{{ item }}</li>
            </ul>
          </dd>
        </template>
        <template v-else-if="entry == 'contacts'">
          <dt class="col-sm-3" :key="entry">Contacts</dt>
          <dd class="col-sm-9" :key="value">
            <template v-for="contact in value">
              <h5 :key="contact">{{ contact.name }}</h5>
              <dl class="row" :key="contact">
                <template v-for="(cv, ce) in contact">
                  <template v-if="ce != 'addresses' && ce != 'name'">
                    <dt class="col-sm-3" :key="ce">{{ ce|camelTitle }}</dt>
                    <dd class="col-sm-9" :key="cv">{{ cv }}</dd>
                  </template>
                </template>
              </dl>
              <template v-for="address in contact.addresses">
                <dl class="row address" :key="address">
                  <template v-for="(av, ae) in address">
                    <dt class="col-sm-3" :key="ae">{{ ae|camelTitle }}</dt>
                    <dd class="col-sm-9" :key="av">{{ av }}</dd>
                  </template>
                </dl>
              </template>
            </template>
          </dd>
        </template>
        <template v-else>
          <dt class="col-sm-3" :key="entry">{{ entry|camelTitle }}</dt>
          <dd class="col-sm-9" :key="value">{{ value }}</dd>
        </template>
      </template>
    </dl>
  </div>
</template>


<script>
export default {
  props: {
    project: Object
  },
  filters: {
    camelTitle(str) {
      str = str
        .replace(/([A-Z])/g, " $1")
        .toLowerCase()
        .split(" ");
      for (let i = 0; i < str.length; i++) {
        str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1);
      }
      return str.join(" ");
    }
  }
};
</script>