import { assert } from 'chai'
import DataHandlerBase from '../../app/base/DataHandlerBase.js'
import { __RewireAPI__ as DHB } from '../../app/base/DataHandlerBase.js'
import Backbone from 'backbone'

describe('base', () => {
  describe('DataHandlerBase', () => {
    describe('constructor', () => {
      it('invokes its own .get_data method', (done) => {
        /***
         * The constructor will be invoked when the class is instantiated.
         * If the constructor calls get_data, then `done` will be called,
         * and the test will pass.
         */
        let DataHandlerBase_ = DataHandlerBase.extend({
          get_data: () => done()
        })

        new DataHandlerBase_()
      })
    })

    describe('get_data', () => {
      it('calls d3.json on its own "url" property', (done) => {
        let urlAccept = 'foo'

        DHB.__Rewire__('d3', {
          json: (url, cb) => {
            if (url === urlAccept) {
              DHB.__ResetDependency__('d3')
              done()
            }
          }
        })

        let DataHandlerBase_ = DataHandlerBase.extend({
          constructor: function () {
            Backbone.Model.apply(this, arguments);
          }
        })

        let dhb = new DataHandlerBase_({
          url: urlAccept
        })

        dhb.get_data()
      })

      it('receives data and sets its raw_data property', () => {
        let dataAccept = 'foo'

        DHB.__Rewire__('d3', {
          json: (url, cb) => {
            cb(undefined, dataAccept)
          }
        })

        let DataHandlerBase_ = DataHandlerBase.extend({
          constructor: function () {
            Backbone.Model.apply(this, arguments);
          },
          clean_data: () => null
        })

        let dhb = new DataHandlerBase_({
          url: 'bar'
        })

        dhb.get_data()

        assert.equal(dataAccept, dhb.get('raw_data'))

        DHB.__ResetDependency__('d3')
      })

      it('triggers dataLoaded when it is done', (done) => {
        DHB.__Rewire__('d3', {
          json: (url, cb) => {
            cb(undefined, null)
          }
        })

        let DataHandlerBase_ = DataHandlerBase.extend({
          constructor: function () {
            Backbone.Model.apply(this, arguments);
          },
          clean_data: () => null
        })

        let dhb = new DataHandlerBase_()

        dhb.on('dataLoaded', () => {
          DHB.__ResetDependency__('d3')
          done()
        })

        dhb.get_data()
      })
    })

    describe('clean_data', () => {
      it('throws (because it is abstract)', () => {
        let DataHandlerBase_ = DataHandlerBase.extend({
          constructor: function () {
            Backbone.Model.apply(this, arguments);
          }
        })

        assert.throws(() => {
          let dhb = new DataHandlerBase_()
          dhb.clean_data()
        })
      })
    })
  })
})
