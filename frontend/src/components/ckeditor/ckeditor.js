// jshint ignore:start
import React from "react";
import PropTypes from "prop-types";
import ReactDOM from "react-dom";
import Button from 'misago/components/button';
//const loadScript = require('load-script'); simply loading ckeditor.js and setup_ckeditor.js from base.html

// var defaultScriptUrl = "https://cdn.ckeditor.com/4.6.2/standard/ckeditor.js";

/**
 * original here: https://github.com/codeslayer1/react-ckeditor/blob/master/src/ckeditor.js
 */
class CKEditor extends React.Component {
  constructor(props) {
    super(props);

    //Bindings
    this.onLoad = this.onLoad.bind(this);

    //State initialization
    this.state = {
      //isScriptLoaded: this.props.isScriptLoaded,
      config: this.props.config
    };
  }

  //load ckeditor script as soon as component mounts if not already loaded
  componentDidMount() {
    //if(!this.props.isScriptLoaded){
    //  loadScript(this.props.scriptUrl, this.onLoad);
    //}else{
    //  this.onLoad();
    //}
    this.onLoad();
  }

  componentWillUnmount() {
    this.unmounting = true;
  }

  onLoad() {
    if (this.unmounting) return;

    this.setState({
      isScriptLoaded: true
    });

    if (!window.CKEDITOR) {
      console.error("CKEditor not found");
      return;
    }

    this.editorInstance = setupCKEditor('editor-textarea', 'post');

    //this.editorInstance = window.CKEDITOR.appendTo(
    //  ReactDOM.findDOMNode(this),
    //  //"#editor-textarea",
    //  this.state.config,
    //  this.props.content
    //);

    //Register listener for custom events if any
    for(var event in this.props.events){
      var eventHandler = this.props.events[event];

      this.editorInstance.on(event, eventHandler);
    }
  }

  render() {
    return (
      <div className="editor-border">
        <textarea
          className="form-control"
          value={this.props.content}
          disabled={this.props.loading}
          id="editor-textarea"
          onChange={this.props.onChange}
          rows="9"
        ></textarea>

        <div className={this.props.activeClass} />

        <div className="editor-footer">
          <div className="buttons-list pull-left"></div>

          <button
            className="btn btn-default btn-sm pull-right"
            disabled={this.props.loading}
            onClick={this.props.onCancel}
            type="button"
          >
            {gettext("Cancel")}
          </button>

          <Button
            className="btn-primary btn-sm pull-right"
            loading={this.props.loading}
          >
            {this.props.submitLabel || gettext("Post")}
          </Button>
        </div>
      </div>
    );
  }
}

CKEditor.defaultProps = {
  content: "",
  config: {},
  isScriptLoaded: false,
  //scriptUrl: defaultScriptUrl,
  activeClass: "",
  events: {}
};

CKEditor.propTypes = {
  content: PropTypes.any,
  config: PropTypes.object,
  isScriptLoaded: PropTypes.bool,
  //scriptUrl: PropTypes.string,
  activeClass: PropTypes.string,
  events: PropTypes.object
};

export default CKEditor;