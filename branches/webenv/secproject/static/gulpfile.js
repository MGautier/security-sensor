var gulp = require('gulp');
var cssnano = require('gulp-cssnano');
var uglify = require('gulp-uglify');

gulp.task('cssnano', function(){
return gulp.src('/home/debian-moises/Documentos/securityproject/branches/webenv/secproject/static/css/*.css')
.pipe(ccsnano())
.pipe(gulp.dest('/home/debian-moises/Documentos/securityproject/branches/webenv/secproject/static/build/css'))
});

gulp.task('uglify', function(){
return gulp.src('/home/debian-moises/Documentos/securityproject/branches/webenv/secproject/static/js/*.js')
.pipe(uglify())
.pipe(gulp.dest('/home/debian-moises/Documentos/securityproject/branches/webenv/secproject/static/build/js/'))
});

gulp.task('nano', ['cssnano', 'uglify']);