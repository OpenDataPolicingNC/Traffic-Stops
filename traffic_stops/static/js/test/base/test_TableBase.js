import { assert } from 'chai'
import TableBase from '../../app/base/TableBase.js'
import { __RewireAPI__ as TB } from '../../app/base/TableBase.js'
import Backbone from 'backbone'

describe('base', () => {
  describe('TableBase', () => {
    let handler = new Backbone.Model()

    describe('constructor', () => {
      it('attaches this.update as a dataLoaded listener to its model', (done) => {
        let TableBase_ = TableBase.extend({
          update: () => done()
        })
        let tb = new TableBase_({ handler })
        handler.trigger('dataLoaded')
      })

      it('attaches this.showError as a dataRequestFailed listener to it smodel', (done) => {
        let TableBase_ = TableBase.extend({
          showError: () => done()
        })
        let tb = new TableBase_({ handler })
        handler.trigger('dataRequestFailed')
      })
    })
  })
})
