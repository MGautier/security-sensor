var gulp = require('gulp');
var nanoCSS = require('gulp-cssnano');
var uglify = require('gulp-uglify');


gulp.task('cssnano', function(){
  return gulp.src('$VIRTUAL_ENV/secproject/static/css/*.css')
    .pipe(nanoCSS())
    .pipe(gulp.dest('$VIRTUAL_ENV/secproject/static/build/css/'));
});

gulp.task('uglify', function(){
  return gulp.src('$VIRTUAL_ENV/secproject/static/js/*.js')
    .pipe(uglify())
    .pipe(gulp.dest('$VIRTUAL_ENV/secproject/static/build/js'));
});

gulp.task('optimized', ['cssnano', 'uglify']);
