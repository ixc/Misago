// jshint ignore:start
import React from 'react';
import SearchForm from './form';
import SideNav from './sidenav';


export default class extends React.Component {

  /* jshint ignore:start */
  getBreadcrumb() {
    return (
      <div className="page-breadcrumbs">
        <div className="container">
          <ol className="breadcrumb hidden-xs">
            <li><a href="/">Home</a></li>
            <li><a href="#">Search</a></li>
          </ol>
        </div>
      </div>
    );
  }
  /* jshint ignore:end */

  render() {
    return (
      <div className="page page-search">
        <div style={{marginTop:40}}>{this.getBreadcrumb()}</div>
        <SearchForm
          provider={this.props.provider}
          search={this.props.search}
          />

        <div className="container">
          <div className="row">
            <div className="col-md-3">
              <SideNav providers={this.props.search.providers}/>
            </div>
            <div className="col-md-9">
              {this.props.children}
              <SearchTime
                provider={this.props.provider}
                search={this.props.search}
                />
            </div>
          </div>
        </div>
      </div>
    );
    /* jshint ignore:end */
  }
}

export function SearchTime(props) {
  let time = null;
  props.search.providers.forEach((p) => {
    if (p.id === props.provider.id) {
      time = p.time;
    }
  });

  if (time === null) return null;

  const copy = gettext("Search took %(time)s s to complete");

  return (
    <footer className="search-footer">
      <p>
        {interpolate(copy, {time}, true)}
      </p>
    </footer>
  );
}