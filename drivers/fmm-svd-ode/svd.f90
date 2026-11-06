! GAMS D6: SVD checked by reconstruction, orthogonality and known spectra.
program check_svd
 use ForsytheMalcolmMoler, only: SVD
 use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
 implicit none
 integer,parameter :: dp=selected_real_kind(10,50)
 integer :: n,m,extra,kind,i,j,k,status,count
 real(dp),allocatable :: a(:,:),original(:,:),u(:,:),v(:,:),w(:),scaled(:,:),gram(:,:)
 real(dp) :: scale,residual,orthogonality,energy,maximum,maximum_orth,maximum_energy,known
 real(dp),parameter :: tolerance=5.e-11_dp
 maximum=0;maximum_orth=0;maximum_energy=0;count=0
 do n=1,4
  do extra=0,2,2
   m=n+extra
   allocate(a(m,n),original(m,n),u(m,n),v(n,n),w(n),scaled(m,n),gram(n,n))
   do kind=1,6
    a=0
    select case(kind)
    case(1)
     do i=1,n
      a(i,i)=i
     end do
    case(2,5,6)
     do j=1,n
      do i=1,m
       a(i,j)=sin(real(3*i+2*j,dp))+0.3_dp*cos(real(i*j,dp))
       if(i==j) a(i,j)=a(i,j)+2
      end do
     end do
     if(kind==5) a=a*1.e-30_dp
     if(kind==6) a=a*1.e30_dp
    case(3)
     a=0
    case(4)
     do j=1,n
      do i=1,m
       a(i,j)=real(i,dp)*real(j,dp)
      end do
     end do
    end select
    original=a
    call SVD(a,w,.true.,u,.true.,v,status)
    if(status/=0) error stop 'SVD status'
    if(any(a/=original)) error stop 'SVD modified input'
    if(.not.all(ieee_is_finite(w)) .or. any(w<0)) error stop 'SVD spectrum'
    if(.not.all(ieee_is_finite(u)) .or. .not.all(ieee_is_finite(v))) error stop 'SVD vectors'
    scale=maxval(abs(original));if(scale==0) scale=1
    do j=1,n
     scaled(:,j)=u(:,j)*(w(j)/scale)
    end do
    residual=maxval(abs(matmul(scaled,transpose(v))-original/scale))
    gram=matmul(transpose(u),u)
    do i=1,n
     gram(i,i)=gram(i,i)-1
    end do
    orthogonality=maxval(abs(gram))
    gram=matmul(transpose(v),v)
    do i=1,n
     gram(i,i)=gram(i,i)-1
    end do
    orthogonality=max(orthogonality,maxval(abs(gram)))
    energy=abs(sum((w/scale)**2)-sum((original/scale)**2))/max(1._dp,sum((original/scale)**2))
    if(kind==1) then
     ! Singular values need not be sorted; compare their power sums with the known diagonal.
     do k=1,3
      known=sum([(real(i,dp)**k,i=1,n)])
      if(abs(sum(w**k)-known)>tolerance*max(1._dp,known)) error stop 'diagonal spectrum'
     end do
    else if(kind==3) then
     if(maxval(abs(w))>tolerance) error stop 'zero spectrum'
    else if(kind==4) then
     known=sqrt(sum([(real(i,dp)**2,i=1,m)])*sum([(real(j,dp)**2,j=1,n)]))
     if(abs(maxval(w)-known)>tolerance*known) error stop 'rank-one spectrum'
     if(sum(w)-maxval(w)>tolerance*known) error stop 'rank-one null spectrum'
    end if
    if(max(residual,orthogonality,energy)>tolerance) error stop 'SVD invariant'
    maximum=max(maximum,residual);maximum_orth=max(maximum_orth,orthogonality);maximum_energy=max(maximum_energy,energy)
    count=count+1
   end do
   deallocate(a,original,u,v,w,scaled,gram)
  end do
 end do
 print '(a,i0)', 'Checked SVD matrices: ',count
 print '(a,es14.6)', 'Maximum scaled reconstruction error: ',maximum
 print '(a,es14.6)', 'Maximum orthogonality error: ',maximum_orth
 print '(a,es14.6)', 'Maximum relative energy error: ',maximum_energy
 print '(a)', 'PASS svd'
end program
