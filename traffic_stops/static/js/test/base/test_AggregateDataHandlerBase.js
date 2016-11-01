import { assert } from 'chai'
import AggregateDataHandlerBase from '../../app/base/AggregateDataHandlerBase.js'
import { __RewireAPI__ as ADHB } from '../../app/base/AggregateDataHandlerBase.js'
import Backbone from 'backbone'

describe('base', () => {
  describe('DataHandlerBase', () => {
    describe('get_data', () => {
      let AggregateDataHandlerBase_ = AggregateDataHandlerBase.extend({
        clean_data: () => true
      })

      it('returns a Promise', () => {
        let adhb = new AggregateDataHandlerBase_({url: 'foo'})
        let result = adhb.get_data()

        assert.isTrue(result instanceof Promise)
      })

      it('aggregates data from all its handlers\' get_data promises', (done) => {
        let [accept1, accept2] = ['accept1', 'accept2']

        let AggregateDataHandlerBase_ = AggregateDataHandlerBase.extend({
          /***
           * Trivial clean_data method that will just pass along the
           * input data so we can verify that this data is received and
           * piped through the cleanup method.
           */
          clean_data: function () {
            this.set('data', this.get('raw_data'))
          }
        })

        let HandlerType = Backbone.Model.extend({
          get_data: function () {
            return new Promise((resolve, reject) => { resolve(this.get('accept')) })
          }
        })

        let adhb = new AggregateDataHandlerBase_({
          url: 'foo'
        , handlers: [
            new HandlerType({accept: accept1})
          , new HandlerType({accept: accept2})
          ]
        })

        let result = adhb.get_data()

        result.then((data) => {
          assert.includeMembers(data, [accept1, accept2])
          done()
        })
      })
    })
  })
})
