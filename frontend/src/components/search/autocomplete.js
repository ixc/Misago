// jshint ignore:start
import React from 'react';
import misago from 'misago';
import ajax from 'misago/services/ajax';

function highlightTextQuery(body, query) {
  const start = body.toLowerCase().indexOf(query.toLowerCase());
  if (start === -1) {
    return [body, '', ''];
  }
  const end = start + query.length;
  return [
      body.slice(0, start),
      body.slice(start, end),
      body.slice(end, body.length),
  ]
}

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.query = props.query;
    this.isLoading = false;
    this.providerId = props.providerId;

    this.state = {
      suggestions: []
    }
  }

  componentWillReceiveProps(props) {
    const prevQuery = this.query;
    const prevProviderId = this.providerId;
    const query = props.query;
    const providerId = props.providerId;
    this.query = query;
    this.providerId = providerId;

    if (prevProviderId !== this.providerId) {
      this.setState({suggestions: []});
    }

    if (query !== prevQuery && query.length > 1) {
      ajax.get(misago.get('SEARCH_AUTOCOMPLETE_API'), {
        q: this.query.trim()
      })
        .then(data => {
          // Bail if the results are no longer relevant
          if (this.query !== query || this.providerId !== providerId) {
            return;
          }

          let relevantData = null;
          data.forEach(obj => {
            if (obj.id === providerId) {
              relevantData = obj;
            }
          });

          if (relevantData) {
            const completions = relevantData.completions;
            const suggestions = completions.map(obj => {
              const text = obj instanceof Array
                ? obj[0]
                : obj;
              const highlighted = highlightTextQuery(text, query);
              const components = (
                <span>
                  {highlighted[0] ? <span>{highlighted[0]}</span> : null}
                  {highlighted[1] ? <strong>{highlighted[1]}</strong> : null}
                  {highlighted[2] ? <span>{highlighted[2]}</span> : null}
                </span>
              );

              return {
                text,
                components
              }
            });
            this.setState({suggestions});
          }
        }).catch(err => {
          this.setState({suggestions: []});
          console.error(err);
        });
    }
  }

  render() {
    if (!this.props.visible || !this.state.suggestions.length) {
      return null;
    }

    return (
      <div className="sac-root">
        <div className="sac-item-list">
          {this.state.suggestions.map((suggestion, i) => {
            return (
              <div
                className="sac-item"
                key={i}
                onClick={() => this.props.onSelect(suggestion.text)}
              >
                {suggestion.components}
              </div>
            );
          })}
        </div>
      </div>
    )
  }
}