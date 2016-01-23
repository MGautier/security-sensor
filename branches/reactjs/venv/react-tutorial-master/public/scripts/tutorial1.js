// tutorial1.js

var CommentBox = React.createClass({
  render: function(){
    return(
        <div className="commentBox">
        Hello, world! I am a commentBox.
        </div>
    );
  }
});

ReactDOM.render(
    <CommentBox />,
  document.getElementById('content')
);
