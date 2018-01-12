import { assert } from 'chai'
import VisualBase from '../../app/base/VisualBase.js'
import { __RewireAPI__ as VB } from '../../app/base/VisualBase.js'
import Backbone from 'backbone'
import $ from 'jquery'

describe('base', () => {
  describe('VisualBase', () => {
    let handler = {
      get_data: () => new Promise((resolve, reject) => resolve(true))
    }

    /***
     * Just to have a clear idea what all the methods are ...
     */

    let Stubbed = VisualBase.extend({
      constructor: function () {
        Backbone.Model.apply(this, arguments);
      },
      setDOM: () => null,
      loader_show: () => null,
      showError: () => null,
      loader_hide: () => null,
      update: () => null,
      drawStartup: () => null,
      drawChart: () => null,
      setDefaultChart: () => null,
    })

    describe('constructor', () => {
      it('binds this.update to its handler\'s get_data Promise resolution', (done) => {
        let accept = true
        let handler = {
          get_data: () => new Promise((resolve, reject) => resolve(accept))
        }
        let VisualBase_ = VisualBase.extend({
          update: (data) => {
            assert.equal(data, accept)
            done()
          },

          setDOM: () => true,
          loader_show: () => true,
          setDefaultChart: () => true,
          showError: () => true
        })

        new VisualBase_({handler})
      })

      it('binds this.showError to its handler\'s get_data Promise rejection', (done) => {
        let accept = true
        let handler = {
          get_data: () => new Promise((resolve, reject) => reject(accept))
        }
        let VisualBase_ = VisualBase.extend({
          showError: (error) => {
            assert.equal(error, accept)
            done()
          },

          setDOM: () => true,
          loader_show: () => true,
          setDefaultChart: () => true,
          update: () => true
        })

        new VisualBase_({handler})
      })

      it('invokes setDOM', (done) => {
        let VisualBase_ = VisualBase.extend({
          setDOM: () => done(),
          loader_show: () => null,
          setDefaultChart: () => null,
          update: () => null,
          showError: () => null
        })

        new VisualBase_({ handler })
      })

      it('invokes loader_show', (done) => {
        let VisualBase_ = VisualBase.extend({
          setDOM: () => null,
          loader_show: () => done(),
          setDefaultChart: () => null,
          update: () => null,
          showError: () => null
        })

        new VisualBase_({ handler })
      })

      it('invokes setDefaultChart', (done) => {
        let VisualBase_ = VisualBase.extend({
          setDOM: () => null,
          loader_show: () => null,
          setDefaultChart: () => done(),
          update: () => null,
          showError: () => null
        })

        new VisualBase_({ handler })
      })
    })

    describe('setDOM', () => {
      let id = 'test_selector'
      let selector = '#' + id

      before(() => {
        $(`<div class="parent"><div id="${ id }"></div></div>`).appendTo($('body'))
      })

      after(() => {
        document.body.innerHTML = ''
      })

      it('assigns its svg and div attributes', () => {
        let VisualBase_ = Stubbed.extend({
          setDOM: VisualBase.prototype.setDOM
        })

        let vb = new VisualBase_({ selector })
        vb.setDOM()

        assert.equal(id, $(vb.svg).attr('id'))
        assert.isTrue($(vb.div).is('.parent'))
      })
    })

    describe('loader_show', () => {
      after(() => {
        document.body.innerHTML = ''
      })

      it('prepends a spinner element to this.div', () => {
        let VisualBase_ = Stubbed.extend({
          loader_show: VisualBase.prototype.loader_show
        })

        let vb = new VisualBase_()
        vb.div = $('<div></div>')
        vb.loader_show()
        assert.isOk(vb.loader_div)
        assert.isOk(vb.div.children().length)
      })
    })

    describe('showError', () => {
      it('invokes loader_hide', (done) => {
        let VisualBase_ = Stubbed.extend({
          showError: VisualBase.prototype.showError,
          loader_hide: () => done()
        })
        let vb = new VisualBase_()
        vb.showError()
      })

      it('prepends a warning element to this.div', () => {
        let VisualBase_ = Stubbed.extend({
          showError: VisualBase.prototype.showError
        })
        let vb = new VisualBase_()
        vb.div = $('<div></div>')
        vb.showError()
        assert.isOk(vb.error_div)
        assert.isOk(vb.div.children().length)
      })
    })

    describe('loader_hide', () => {
      it('kills its loader_div element', () => {
        let VisualBase_ = Stubbed.extend({
          loader_hide: VisualBase.prototype.loader_hide
        })
        let vb = new VisualBase_()
        vb.loader_div = $('<div className="fail"></div>')
        vb.loader_hide()
        assert.equal(0, $('.fail').length)
      })
    })

    describe('update', () => {
      it('invokes loader_hide, drawStartup, drawChart', () => {
        let counter = []
        let updater = () => counter.push('updated')
        let VisualBase_ = Stubbed.extend({
          update: VisualBase.prototype.update,
          loader_hide: updater,
          drawStartup: updater,
          drawChart: updater
        })
        let vb = new VisualBase_()
        vb.update('data')
        assert.equal(3, counter.length)
      })
    })
  })
})
