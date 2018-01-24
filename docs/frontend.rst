Organization of the front-end
=============================

Overview
--------

The front-end code for the graphs on the Open Data Policing site is broken down into three groups.

- base: classes that define the shared functionality of all components. These include:
    - ``DataHandlerBase``: the Model subclass that handles talking to the API
    - ``AggregateDataHandlerBase``: used for supplying data to graphs that combine multiple sources
    - ``VisualBase``: the Model subclass that handles the graph-specific data processing and D3-based rendering for each graph
    - ``TableBase``: like ``VisualBase`` but specific to tables
- common: classes that define the specific graphs, factoring out the code that's shared across states; graphs for particular states are configured by subclassing these ``common`` components and replacing their abstract methods
- states: subclasses of ``common`` components configured for individual states

How these components interact is the subject of the rest of these docs.

Putting the pieces together
---------------------------

In the ``agency_detail.html`` template for individual states, you will see a ``script`` block within ``{% block graph-code %}`` containing a number of variable declarations along these lines::

    var stop_handler = new MD.StopsHandler({url: "{% url 'md:agency-api-stops' object.pk %}?officer={{officer_id|urlencode}}"});

Beneath these, there are object creation statements referring to these variables, like this::

    new MD.StopRatioDonut({handler: stop_handler, selector: "#stop_race_pie"});

These two statements, in combination, create a graph on the page. The ``Handler`` component connects to the API using the supplied values; it invokes its own ``clean_data`` method, which must be defined for each particular ``Handler`` subclass; and it triggers an event when the loading and cleaning are completed.

The graph component (here, ``StopRatioDonut``) listens for its associated Handler's event and invokes its ``update`` method, defined on ``VisualBase``, which sets off a cascade of other methods that handle the visual behavior of the graph.

Each subclass of ``VisualBase`` needs to define at least these methods:

- ``drawStartup``: DOM manipulation steps that precede the drawing of the chart (e.g. creating and appending elements that are parameterized by the received data)
- ``setDefaultChart``: setting the ``this.chart`` value to an NVD3 chart with correct configuration values
- ``drawChart``: calling ``this.chart`` to actually mount and draw the chart with the data


Understanding "common" classes
------------------------------

Almost all of the code can be shared between states. There are exceptions, however; and the ``common`` classes are defined so that these exceptions can be handled gracefully. Parameterization for particular states is, in general, handled by means of abstract methods that calculate state-specific values.

Let's look at ``StopRatioDonutBase`` as a concrete example. This has two abstract methods:

- ``_items``: the items to display on the chart
- ``_pprint``: a function used to format ("pretty-print") item names for display

The North Carolina instance of this class defines them like this::

    _items: function () {
      return (this.get('showEthnicity')) ? Stops.ethnicities : Stops.races;
    },

    _pprint: function (type) {
      return Stops.pprint.get(type);
    }

So when ``_items`` is invoked, it fetches its ``showEthnicity`` value and returns either ``Stops.ethnicities`` or ``Stops.races``. When ``_pprint`` is used, it looks up a value in ``Stops.pprint``.

The Maryland instance is much simpler::

    _items: function () {
      return Stops.ethnicities;
    },

    _pprint: function (x) {
      return x;
    }

Because Maryland has no race / ethnicity distinction, its items are simply ``Stops.ethnicities``. And because its data is "humanized" from the get-go, its ``_pprint`` function can just return the input value.

Other configuration
-------------------

Using state code
~~~~~~~~~~~~~~~~

Each state has an ``index.js`` file that makes each data handler and piece of graph code globally available so that it can be executed in templates. This works by importing each value and splicing it into an object at ``window.<state-abbreviation>``, like so::

    import Stops from './defaults.js';
    import StopsGraphs from './Stops.js';
    import StopSearch from './StopSearch.js';

    if (typeof window.MD === 'undefined') window.MD = {};

    Object.assign(window.MD,
      {Stops},
      StopsGraphs,
      StopSearch
    )

Other configuration
~~~~~~~~~~~~~~~~~~~

Each state also has a configuration file in ``defaults.js``. For historical reasons, this exports a value usually referred to as ``Stops`` (this somewhat confusing name is how we inherited it, and this is how it still is!).

Many ``common`` classes refer to ``Stops``, and it needs to be defined for each state, as well as included in ``index.js``.
