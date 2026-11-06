! Catalog-owned numerical checks; upstream numerical sources are downloaded separately.
program check_linear
  use ndsm_root, only: fp, it, mg_ptr, debug
  use ndsm_interp, only: ninterp
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  integer(it) :: ndim, shape(3), nsize, k, j, index, rem, axis
  integer :: trial, checked
  type(mg_ptr) :: mesh(3)
  real(fp), allocatable :: f(:)
  real(fp) :: q(3), x(3), want, got, err, maximum
  real(fp), parameter :: tol=5.e-13_fp
  debug=.false.
  checked=0
  maximum=0
  do ndim=1_it,1_it
    shape=[4_it,5_it,3_it]
    nsize=product(shape(:ndim))
    do axis=1,ndim
      ! Different spacing per axis; nondefault mesh bounds exercise internal remapping.
      allocate(mesh(axis)%val(-2:shape(axis)-3))
      do j=0,shape(axis)-1
        mesh(axis)%val(j-2)=-0.5_fp*axis+0.25_fp*axis*j
      end do
    end do
    allocate(f(nsize))
    do k=1,nsize
      rem=k-1
      x=0
      do axis=1,ndim
        index=mod(rem,shape(axis)); rem=rem/shape(axis)
        x(axis)=mesh(axis)%val(index-2)
      end do
      f(k)=known(ndim,x)
    end do
    ! Tensor product of endpoint, node, interior and exterior coordinates.
    do trial=0,5**int(ndim)-1
      rem=trial
      q=0
      do axis=1,ndim
        j=mod(rem,5_it); rem=rem/5
        select case(j)
        case(0); q(axis)=mesh(axis)%val(-2)
        case(1); q(axis)=mesh(axis)%val(shape(axis)-3)
        case(2); q(axis)=mesh(axis)%val(-1)
        case(3); q(axis)=mesh(axis)%val(-2)+0.37_fp*axis
        case(4); q(axis)=mesh(axis)%val(-2)-0.1_fp*axis
        end select
      end do
      want=known(ndim,q)
      got=ninterp(ndim,nsize,shape(:ndim),mesh(:ndim),q(:ndim),f)
      if (.not.ieee_is_finite(got)) error stop 'nonfinite interpolation'
      err=abs(got-want)/max(1._fp,abs(want))
      maximum=max(maximum,err)
      if (err>tol) error stop 'interpolation mismatch'
      checked=checked+1
    end do
    ! A non-affine nodal table distinguishes piecewise-linear evaluation from a global fit.
    f=[0.25_fp,0.0625_fp,0._fp,0.0625_fp]
    do trial=1,2
      if(trial==1) then
        q(1)=-0.375_fp; want=0.15625_fp
      else
        q(1)=-0.6_fp; want=0.325_fp
      end if
      got=ninterp(ndim,nsize,shape(:ndim),mesh(:ndim),q(:ndim),f)
      if (.not.ieee_is_finite(got)) error stop 'nonfinite tabular interpolation'
      err=abs(got-want)
      maximum=max(maximum,err)
      if(err>tol) error stop 'piecewise tabular mismatch'
      checked=checked+1
    end do
    deallocate(f)
    do axis=1,ndim
      deallocate(mesh(axis)%val)
    end do
  end do
  print '(a,i0)', 'Known-value checks: ',checked
  print '(a,es14.6)', 'Maximum normalized error: ',maximum
  print '(a)', 'PASS linear'
contains
  pure function known(n,x) result(y)
    integer(it), intent(in) :: n
    real(fp), intent(in) :: x(3)
    real(fp) :: y
    y=1.25_fp-0.7_fp*x(1)
    if(n>=2) y=y+0.4_fp*x(2)+0.6_fp*x(1)*x(2)
    if(n>=3) y=y-0.3_fp*x(3)+0.2_fp*x(1)*x(3)-0.5_fp*x(2)*x(3)+0.8_fp*x(1)*x(2)*x(3)
  end function
end program
