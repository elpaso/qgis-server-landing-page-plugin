<template>
  <div class="card-text">
    <dl class="row">
      <template v-for="(value, entry) in project.metadata">
        <template v-if="entry == 'links'">
          <dt class="col-sm-3" :key="uniqueKey(entry + 'k')">{{ entry }}</dt>
          <dd class="col-sm-9" :key="uniqueKey(entry + 'v')">
            <ul v-for="item in value" :key="uniqueKey(item.url)">
              <li>
                <a :href="item.url">{{ item.name }}</a>
                &mdash; {{ item.description }}
              </li>
            </ul>
          </dd>
        </template>
        <template v-else-if="entry == 'categories' || entry == 'history'">
          <dt class="col-sm-3" :key="uniqueKey(entry + 'k')">{{ entry|camelTitle }}</dt>
          <dd class="col-sm-9" :key="uniqueKey(entry + 'v')">
            <ul v-for="item in value" :key="uniqueKey(item)">
              <li :key="uniqueKey(item)">{{ item }}</li>
            </ul>
          </dd>
        </template>
        <template v-else-if="entry == 'contacts'">
          <dt class="col-sm-3" :key="uniqueKey(entry + 'k')">Contacts</dt>
          <dd class="col-sm-9" :key="uniqueKey(entry + 'v')">
            <template v-for="contact in value">
              <h5 :key="uniqueKey(contact.name)">{{ contact.name }}</h5>
              <dl class="row" :key="uniqueKey(contact.name)">
                <template v-for="(cv, ce) in contact">
                  <template v-if="ce != 'addresses' && ce != 'name'">
                    <dt class="col-sm-3" :key="uniqueKey(ce)">{{ ce|camelTitle }}</dt>
                    <dd class="col-sm-9" :key="uniqueKey(cv)">{{ cv }}</dd>
                  </template>
                </template>
              </dl>
              <template v-for="address in contact.addresses">
                <dl class="row address" :key="uniqueKey(address.name)">
                  <template v-for="(av, ae) in address">
                    <dt class="col-sm-3" :key="uniqueKey(ae)">{{ ae|camelTitle }}</dt>
                    <dd class="col-sm-9" :key="uniqueKey(av)">{{ av }}</dd>
                  </template>
                </dl>
              </template>
            </template>
          </dd>
        </template>
        <template v-else>
          <dt class="col-sm-3" :key="uniqueKey(entry)">{{ entry|camelTitle }}</dt>
          <dd class="col-sm-9" :key="uniqueKey(value)">{{ value }}</dd>
        </template>
      </template>
    </dl>
  </div>
</template>


<script>
const uuidv4 = require("uuid/v4");

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
  },
  data: function() {
    return {
      uniqueKey: function(value) {
        return uuidv4() + value;
      }
    };
  }
};
</script>